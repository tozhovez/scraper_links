import os
import asyncio
from pprint import pprint
from urllib.parse import urlparse
from tools.page_parser import spider_loader
from tools.async_loader import Loader, LoaderError, LoaderContentTypeError
from tools.aiofiles_lib import create_dir, read_from_json_file, write_to_json_file
from tools.postgres_queries import PG
from codetiming import Timer

pg_client = PG()


class DomainEmptyTypeError(Exception):
    pass



class Task:
    def __init__(self, initial_url, max_depth, tasks_dir):
        self.initial_url = initial_url
        self.max_depth = max_depth
        self.initial_domain = self.exstract_initial_domain()
        self.links = {}
        self.tasks = []
        self.num_workers = 8
        self.queue = asyncio.Queue(maxsize=self.num_workers)
        self.tasks_dir = tasks_dir
        self.task_id = None
        self.task_dir = None
        self.links_file = None
        self.task_file = None


    def exstract_initial_domain(self):
        t = urlparse(self.initial_url)
        if t.netloc:
            return t.netloc
        else:
            raise DomainEmptyTypeError(f"{self.initial_url} empty domain")


    async def setup_settings(self):
        self.task_id =  await pg_client.get_task_id(self.initial_url, self.max_depth)
        self.task_dir = os.path.join(self.tasks_dir, str(self.task_id))
        self.links_file = os.path.join(self.task_dir, "links.txt")
        self.task_file = os.path.join(self.task_dir, "task.txt")
        await create_dir(self.tasks_dir)
        await create_dir(self.task_dir)
        self.links = await read_from_json_file(self.links_file) or self.links
        self.tasks = await read_from_json_file(self.task_file) or self.tasks
        if not self.tasks:
            self.tasks.append((self.initial_domain, self.max_depth, self.initial_url, self.initial_url, 0))

    async def put_task_to_work_queue(self):
        #
        for work in self.tasks:
            print(work)
            await self.queue.put(work)
    

    async def start_workers(self, loop):
        
        loop_tasks = []
        with Timer(text="\nIn put_task_to_work_queue Total elapsed time: {:.1f}"):
            for w in range(self.num_workers):
                print(f"creating task {w}")
                task = loop.create_task(self.spider_task(f"{w}"))

                loop_tasks.append(task)
               






    async def spider_task(self, name):

        timer = Timer(text=f"Task {name} elapsed time: {{:.1f}}")
        while not self.queue.empty():
            try:
                work = await self.queue.get()
                print(work)
                print(f"{name} running task {work}")
                timer.start()
                await self.spyder(work)
                timer.stop()
                
            except asyncio.CancelledError:
                print('task_func was canceled')
                raise
        return 'the result'


    def task_canceller(self, t):
        print('in task_canceller')
        t.cancel()
        print('canceled the task')



    async def run_spider(self, loop):
        await self.setup_settings()

        await self.start_workers(loop)
        await self.put_task_to_work_queue()

        



    def start_spider(self):
        event_loop = asyncio.get_event_loop()
        try:
            event_loop.run_until_complete(self.run_spider(event_loop))
        finally:
            event_loop.close()






    async def spider(self, work):

       
        base_url, max_depth, source_url, url, depth = work
        data = await spyder_loader(base_url, max_depth, source_url, url, depth)
        if data:
            if data["source_url"] and data["url"]:
                if data["source_url"] in self.links:
                    self.links[data["source_url"]].append(data["url"])
                else:
                    self.links[data["source_url"]]=[data["url"],]
               
            if data["depth"]<= self.max_depth:
                for k in data["all_links"]:
                    if k['real_link'] in self.links:
                            continue
                    if k['domain_link'] == self.initial_domain:
                        self.tasks.append((self.initial_domain, self.max_depth, data["url"], k['real_link'], depth+1))
                        
            print(len(self.tasks))

