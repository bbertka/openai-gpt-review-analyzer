#!/usr/bin/python3

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker
from datetime import timedelta
import uuid, time, os
import logging

#For Docker/Kuberntes
#temporal_host = os.getenv("TEMPORAL_HOST")
#temporal_port = os.getenv("TEMPORAL_PORT")

#For testing
temporal_host = "192.168.1.114"
temporal_port = "7233"



# Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


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

            logger.info(f"Item: {item}, Overall Product Sentiment: {result}, {verdict}")
        except Exception as e:
            logger.exception("Failed to execute workflow")
        
        return result, verdict


if __name__ == '__main__':
    logger.info("Review Analyzer is starting up...")
    try:
        with workflow.unsafe.imports_passed_through():
            from routes import CFWorker
        worker = CFWorker(port=os.getenv("PORT"))
        worker.start()
        logger.info("Review Analyzer has started successfully!")
        while True:
            time.sleep(60)
            logger.info("Review Analyzer is listening...")
    except Exception as e:
        logger.exception("An error occurred while starting the Review Analyzer")
    finally:
        worker.join()
