
import configparser

class PumpDetector:
   
    def __init__(self, system_prompt = None):

        self.system_prompt = system_prompt
        self.model = None
        
    @classmethod
    def _read_text_from_file(cls, path):
        
        if path:
            with open(path, 'r') as f:
                text = ''.join(f.readlines())
            return text

        return None

    @classmethod
    def from_prompt_path(cls, path = '', exchange = None, **kwargs):

        system_prompt = cls._read_text_from_file(path)  

        if exchange:
            system_prompt = system_prompt.replace('||EXCHANGE||', str(exchange))


        return cls(
                system_prompt = system_prompt,
                **kwargs 
                )

    def prompt_model(self, data = []):
        """
        Call the model's API with the user prompt and the data 

        Parameters:
        ----------
        prompt: str
            The prompt to the model
        data (Optional): Iterable[str] 
            Extra data to be passed to the model

        Returns: 
        ----------
        str: The model's response
        """
        raise NotImplementedError(f"The function '_prompt_model' needs to be implemented by {self.__class__.__name__}")
    


class GeminiDetector(PumpDetector):

    def __init__(self, api_key, system_prompt = None):
        
        super().__init__(system_prompt = system_prompt)
        
        # Import here so it is not necessary to have this package istalled in case any other detector is used
        import google.generativeai as genai
        genai.configure(api_key = api_key)
        self.model = genai.GenerativeModel(
                model_name = "gemini-1.5-flash",
                system_instruction = self.system_prompt 
                )


    def prompt(self, data = []):

        result = self.model.generate_content(
            data
        )
        return result.text





if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')


    detector  = GeminiDetector.from_prompt_path(
            api_key = config['gemini-flash']['API_KEY'],
            path = 'prompts/coin-prompt.txt',
        )
    
    messages = []
    while True:

        message = input('Enter message: ')
        messages.append(message)
        print(detector.prompt(messages))
    
    # Do this for the coin detection model






