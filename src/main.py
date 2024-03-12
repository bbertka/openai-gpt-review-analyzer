#!/usr/bin/python3

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta
import uuid, time, os


#temporal_host = os.getenv("TEMPORAL_HOST")
#temporal_port = os.getenv("TEMPORAL_PORT")

#For testing
temporal_host = "192.168.1.114"
temporal_port = "7233"

   
@workflow.defn
class ScraperWorkflow:
    @workflow.run
    async def run(self, item: str):
        with workflow.unsafe.imports_passed_through():
            import scrape as scraper
            import analyze as analyzer
          
        itemkeys =  await workflow.execute_activity(
            scraper.scrape,
            item,
            start_to_close_timeout=timedelta(seconds=20)
        )

        result,verdict =  await workflow.execute_activity(
            analyzer.analyze,
            itemkeys,
            start_to_close_timeout=timedelta(seconds=20)
        )
        
        return result, verdict

    
    
async def runner(item: str):
    with workflow.unsafe.imports_passed_through():
        import scrape as scraper
        import analyze as analyzer
    connection_str = "%s:%s" % (temporal_host, temporal_port)
    item = item
    client = await Client.connect(connection_str)
    async with Worker(
        client,
        task_queue="scraper-task-queue",
        workflows=[ScraperWorkflow],
        activities=[scraper.scrape,
                    analyzer.analyze]
    ):
        try:
            flowid = item+"-"+str(uuid.uuid4())[:8]
          
            result, verdict = await client.execute_workflow(
                ScraperWorkflow.run,
                item,
                id=("review-scraper-%s" % flowid),
                task_queue="scraper-task-queue",
            )

            print (f"Item: {item}, Overall Product Sentiment: {result}, {verdict}")
        except Exception as e:
            print("main: Exception: %s" % e)
        
        return result, verdict


if __name__ == '__main__':
    with workflow.unsafe.imports_passed_through():
        from routes import CFWorker
    worker = CFWorker(port=os.getenv("PORT"))
    worker.start()
    print("Review Analyzer has started successfully!")
    while True:
        time.sleep(60)
        print("Review Analyzer is listening...")

    worker.join()