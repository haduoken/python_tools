class DataConvert:
    def __init__(self, out_list, in_list):
        self.out_list = out_list
        self.in_list = in_list
    
    def out_to_in(self, data):
        data = float(data)
        for cur, data_range in enumerate(self.out_list):
            if min(data_range) <= data <= max(data_range):
                _out = self.out_list[cur]
                _in = self.in_list[cur]
                data = (data - _out[0]) / (_out[1] - _out[0]) * (_in[1] - _in[0]) + _in[0]
                return int(round(data))
    
    def in_to_out(self, data):
        data = float(data)
        for cur, data_range in enumerate(self.in_list):
            if min(data_range) <= data <= max(data_range):
                _out = self.out_list[cur]
                _in = self.in_list[cur]
                data = (data - _in[0]) / (_in[1] - _in[0]) * (_out[1] - _out[0]) + _out[0]
                return int(round(data))
