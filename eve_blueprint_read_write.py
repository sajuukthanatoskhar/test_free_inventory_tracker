import http



class blueprint():
    def __init__(self, id):
        self.id = id
        self.name = self.get_name()
        self.materials_req = self.get_mat_reqs()

    def get_mat_reqs(self):
        pass

    def get_name(self):
        pass







