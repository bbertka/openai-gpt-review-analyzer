#!/usr/bin/python3

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from dataclasses import dataclass
from datetime import timedelta
import logging, uuid, time


@dataclass
class SentimentInput:
    item: str
    rating: str
    title: str
    content: str

@workflow.defn
class SentimentWorkflow:
    @workflow.run
    async def run(self, row: SentimentInput):  
        with workflow.unsafe.imports_passed_through():
            import analyze as analyzer
        stars =  await workflow.execute_activity(
            analyzer.star_rating,
            row.rating,
            start_to_close_timeout=timedelta(seconds=20),
        )
        title =  await workflow.execute_activity(
            analyzer.sentiment,
            row.title,
            start_to_close_timeout=timedelta(seconds=20),
        )
        content =  await workflow.execute_activity(
            analyzer.sentiment,
            row.content,
            start_to_close_timeout=timedelta(seconds=20),
        )
        ratings = [stars, title, content]
        rating =  await workflow.execute_activity(
            analyzer.quantify,
            ratings,
            start_to_close_timeout=timedelta(seconds=20),
        )
        verdict =  await workflow.execute_activity(
            analyzer.interprete,
            rating,
            start_to_close_timeout=timedelta(seconds=20),
        )
        print("Item: %s, computing weighted review vector: %s, as: %s" % (row.item, ratings, verdict) )
        return rating


async def runner(item: str):
    with workflow.unsafe.imports_passed_through():
        import analyze as analyzer
        import scrape as scraper
    #logging.basicConfig(level=logging.INFO)
    client = await Client.connect("temporal.home.lab:7233")
    async with Worker(
        client,
        task_queue="sentiment-task-queue",
        workflows=[SentimentWorkflow],
        activities=[analyzer.star_rating, 
                    analyzer.sentiment, 
                    analyzer.quantify, 
                    analyzer.interprete],
    ):
        i = 0
        total = 0
        try:
            flowid = item+"-"+str(uuid.uuid4())[:8]
            df = scraper.scrape(item)
            for row in df.itertuples(index=False):               
                bundle = SentimentInput(item=item, 
                                        rating=row.rating,
                                        title=row.title,
                                        content=row.content )
                rating = await client.execute_workflow(
                    SentimentWorkflow.run,
                    bundle,
                    id=("review-analyzer-%s" % flowid),
                    task_queue="sentiment-task-queue",
                )
                total = total + rating
                i = i+1
            result = float(total/i)
            verdict = await analyzer.interprete(result)
        except Exception as e:
            print("main: Exception: %s" % e)
            result = 0.0
            verdict = "Unavailable"
        if not result or not verdict:
            result = 0.0
            verdict = "Unavailable"
        print (f"Item: {item}, Overall Product Sentiment: {result}, {verdict}")
        return result, verdict


if __name__ == '__main__':
    with workflow.unsafe.imports_passed_through():
        from routes import CFWorker
    worker = CFWorker(port=8000)
    worker.start()
    print("Review Analyzer has started successfully!")
    while True:
        time.sleep(60)
        print("Review Analyzer is listening...")

    worker.join()