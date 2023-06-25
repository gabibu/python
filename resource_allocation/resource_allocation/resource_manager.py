
from datetime import datetime, timedelta
from heapq import heappop, heappush
from typing import List

from resource_allocation.entities.allocation import Allocation
from resource_allocation.entities.room import Room
from resource_allocation.entities.anesthesiologist import Anesthesiologist
from resource_allocation.entities.surgery import Surgery

class ResourceManager:


    def __init__(self, number_of_rooms: int, different_rooms_min_gap: int):
        self._h = []
        self._available_anesthesiologist = []
        self._available_rooms = {i: Room(i, None) for i in range(number_of_rooms)}
        self._anesthesiologist_counter = 0
        self._different_rooms_min_gap = different_rooms_min_gap

    def _rearrange_resources(self, start_time: datetime) -> []:
        if len(self._h) == 0:
            return self._h
        elif self._h[0].end_time > start_time:
            return self._h

        allocation = heappop(self._h)

        self._available_anesthesiologist.append(allocation.anesthesiologist)
        self._available_rooms[allocation.room.room_id] = allocation.room

        return self._rearrange_resources(start_time)

    def _allocate(self, allocation: Allocation, end_time: datetime):

        heappush(self._h, allocation)

        anesthesiologist = [d for d in self._available_anesthesiologist if d == allocation.anesthesiologist][0]

        anesthesiologist.last_allocated_room_id = allocation.room.room_id
        anesthesiologist.last_completed_surgery_time = end_time

        self._available_anesthesiologist.remove(anesthesiologist)

        room = allocation.room
        room.availabe_time = end_time

        del self._available_rooms[room.room_id]

    def _create_new_anesthesiologist(self) -> Anesthesiologist:
        anesthesiologist = Anesthesiologist(anesthesiologists_id=self._anesthesiologist_counter)
        self._anesthesiologist_counter += 1

        self._available_anesthesiologist.append(anesthesiologist)
        return anesthesiologist


    def _assign_to_available_anesthesiologist(self, surgery: Surgery ):

        for anesthesiologist in self._available_anesthesiologist:

            if anesthesiologist.last_completed_surgery_time is not None:
                if surgery.start_time - anesthesiologist.last_completed_surgery_time < timedelta(minutes=self._different_rooms_min_gap):
                    continue

            for room in self._available_rooms.values():
                allocation = Allocation(surgery_id=surgery.surgery_id,
                                        room=room, anesthesiologist=anesthesiologist, end_time=surgery.end_time,
                                        start_time=surgery.start_time)

                self._allocate(allocation, surgery.end_time)
                return allocation


        return None


    def allocate_resources(self, surgeries: List[Surgery]) -> List[Allocation]:

        allocations = []

        for (ii, surgery) in enumerate(surgeries):
            start_time = surgery.start_time
            end_time = surgery.end_time

            self._rearrange_resources(start_time)

            valid_anesthesiologist = None
            valid_room = None

            for anesthesiologist in self._available_anesthesiologist:
                if anesthesiologist.last_allocated_room_id is not None:
                    if anesthesiologist.last_allocated_room_id in self._available_rooms:
                        valid_anesthesiologist = anesthesiologist
                        valid_room = self._available_rooms[anesthesiologist.last_allocated_room_id]
                        break

            if valid_room is not None:
                allocation = Allocation(surgery_id=surgery.surgery_id, room=valid_room,
                                        anesthesiologist=valid_anesthesiologist, end_time=end_time,
                                        start_time=start_time)

                self._allocate(allocation, end_time)

                allocations.append(allocation)

            else:

                allocation = self._assign_to_available_anesthesiologist(surgery)

                if allocation is None:

                    _ = self._create_new_anesthesiologist()

                    allocation = self._assign_to_available_anesthesiologist(surgery)

                    if allocation is None:
                        raise Exception('Allocation cant be none after adding new anesthesiologist')

                    allocations.append(allocation)

                else:
                    allocations.append(allocation)


        return allocations
