from Types import QueueTracks


class PlayerEngine:
    def __init__(self):
        self.queues : list[QueueTracks] = [ ]
    
    async def conntion(self, voice_id)->QueueTracks:
        for queue in self.queues:
            if queue.voice_id == voice_id:
                return queue
            
        new_queue = QueueTracks(voice_id)
        self.queues.append(new_queue)
        return new_queue
    
    async def disconnect(self, voice_id):
        for queue in self.queues:
            if queue.voice_id == voice_id:
                self.queues.remove(queue)
                break
    

