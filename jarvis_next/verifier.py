class ResultVerifier:
    def verify(self,step,data):
        if data is None:
            return False,"no result data"
        if isinstance(data,dict) and data.get("success") is False:
            return False,"result reports success=false"
        return True,None
