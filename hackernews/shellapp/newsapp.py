
from shellapp.newsclients.newservice import NewService
from shellapp.entities.appstates import AppState
from shellapp.textprobs.technologyprobs import TechnologiesProbs
from shellapp.common import apptext

class NewsApp:

    TOP_STORIES_COMMAND = "top stories"
    TECHNOLOGIES_LIST_COMMAND = "technologies"
    EXIT_COMMAND = "exit"


    def __init__(self, news_service: NewService, technologies_probs: TechnologiesProbs):
        self._news_service = news_service
        self._technologies_probs = technologies_probs


    def present_commands(self):

        return apptext.SELECT_COMMAND_FORMAT.format('\n'.join( [NewsApp.TOP_STORIES_COMMAND, NewsApp.TECHNOLOGIES_LIST_COMMAND,
                                                      NewsApp.EXIT_COMMAND]))


    def run(self):

        state = AppState.NO_STATE

        while True:

            if state == AppState.NO_STATE:
                print(self.present_commands())

            cmd = input('> ')

            if cmd == NewsApp.EXIT_COMMAND:
                break

            if state == AppState.NO_STATE:
                if cmd == NewsApp.TOP_STORIES_COMMAND:
                    top_stories = self._news_service.get_top_stories()

                    top_stories = '\n'.join(
                        ['{}) {}'.format(top_story.item_rank, top_story.title if top_story.title is not None else 'N/A') for
                         top_story in top_stories])

                    print(top_stories)
                elif cmd == NewsApp.TECHNOLOGIES_LIST_COMMAND:
                    print(apptext.SELECT_TECHNOLOGY_FORMAT.format(','.join(self._technologies_probs.technologies())))
                    state = AppState.SELECT_TECHNOLOGY
                else:
                    print(apptext.INVALID_INPUT)
            else:
                if cmd in self._technologies_probs.technologies():
                    prob = self._technologies_probs.get_technology_prob(cmd)
                    print(apptext.MONTHLY_PROB_FORMAT.format(cmd, prob))
                    state = AppState.NO_STATE
                else:
                    print(apptext.INVALID_INPUT_FOR_TECHNOLOGY)



