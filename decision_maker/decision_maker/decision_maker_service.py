import argparse
from dependency_injector.wiring import Provide, inject

from decision_maker.decision_maker_container import DecisionMakerContainer
from decision_maker.decision_maker_manager import DecisionMakerManager


@inject
def main(service: DecisionMakerManager = Provide[DecisionMakerContainer.decision_maker]):
    service.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--days_window", type=int, default=10, required=False)
    parser.add_argument("--valid_for_intersection_threshold", type=float, default=0.5, required=False)
    parser.add_argument("--min_identification_days", type=int, default=5, required=False)

    args = parser.parse_args()
    container = DecisionMakerContainer()
    container.config.days_window.from_value(args.days_window)
    container.config.valid_for_intersection_threshold.from_value(args.valid_for_intersection_threshold)
    container.config.min_identification_days.from_value(args.min_identification_days)

    container.wire(modules=[__name__])

    main()
