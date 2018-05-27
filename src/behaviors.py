class humanoid():
    def __init__(self, obj_art, behavior_def=None):
        self.obj_art = obj_art

    def find_loc(self):
        self.loc = self.obj_art.get_rect() 