
import argparse

from shellapp.newsclients.newservice import NewService
from shellapp.newsclients.hackernewsapiclient import HackerNewsAPIClient
from shellapp.newsapp import NewsApp
from shellapp.textprobs.technologyprobs import TechnologiesProbsFactory


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='hackernews shellapp')
    parser.add_argument('-probs_file_path', help='path to probs file', required=False, default='./data/technology_prob.parquet')
    parser.add_argument('-number_of_top_stories', help='number of top stories to show', type=int, required=False,
                        default=40)

    args = parser.parse_args()

    technoplogirs_probs = TechnologiesProbsFactory.build(args.probs_file_path)

    news_service = NewService(HackerNewsAPIClient(), args.number_of_top_stories)
    app = NewsApp(news_service, technoplogirs_probs)

    app.run()



