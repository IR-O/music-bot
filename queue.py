from collections import deque
import asyncio

class Queue:
    def __init__(self):
        self.queues = {}
        self.locks = {}

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    async def put(self, chat_id, file_path, song_info):
        async with self.get_lock(chat_id):
            if chat_id not in self.queues:
                self.queues[chat_id] = deque()
            self.queues[chat_id].append({
                'file': file_path,
                'info': song_info
            })
            return len(self.queues[chat_id])

    async def get(self, chat_id):
        async with self.get_lock(chat_id):
            if chat_id in self.queues and self.queues[chat_id]:
                return self.queues[chat_id].popleft()
            return None

    async def clear(self, chat_id):
        async with self.get_lock(chat_id):
            if chat_id in self.queues:
                self.queues[chat_id].clear()

    async def is_empty(self, chat_id):
        async with self.get_lock(chat_id):
            if chat_id in self.queues:
                return len(self.queues[chat_id]) == 0
            return True

    async def size(self, chat_id):
        async with self.get_lock(chat_id):
            if chat_id in self.queues:
                return len(self.queues[chat_id])
            return 0

    async def task_done(self, chat_id):
        async with self.get_lock(chat_id):
            if chat_id in self.queues:
                self.queues[chat_id].popleft() if self.queues[chat_id] else None

queue = Queue()
