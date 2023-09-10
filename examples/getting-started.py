from stockfish import Stockfish
import json

class StructuredStockfish(Stockfish):
    
    def _structuredEval(self) -> None: 
        self._put("structuredEval")

    def _structuredGo(self) -> None: 
        self._put(f"structuredGo depth {self.depth}")        

    def get_lines(self) -> dict: 
        self._structuredGo()        
        return self._get_structured_data_from_sf_popen_process()
    
    def get_eval(self) -> dict: 
        self._structuredEval()
        return self._get_structured_data_from_sf_popen_process()
    
    def _get_structured_data_from_sf_popen_process(self) -> dict:
        
        data = {}
        while True:
            text = self._read_line()
            if text.startswith("{"):
                data = json.loads(text)
                break
        
        return data

    
    
# engine = StructuredStockfish(
#     path='./StructuredStockfish', # <- make sure that this is the StructuredStockfish binary
#     depth=16,
#     parameters={
#         "MultiPV": 2
#     }
# )


















