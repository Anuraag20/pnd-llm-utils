
import configparser

class PumpDetector:
   
    def __init__(self, coin_prompt = None, schedule_prompt = None):


        self.coin_prompt = coin_prompt
        self.schedule_prompt = schedule_prompt
        self.model = None
        
    @classmethod
    def _read_text_from_file(cls, path):
        
        if path:
            with open(path, 'r') as f:
                text = ''.join(f.readlines())
            return text

        return None

    @classmethod
    def from_prompt_path(cls, schedule_prompt_path = '', coin_prompt_path = '', **kwargs):

        schedule_prompt = cls._read_text_from_file(schedule_prompt_path)
        coin_prompt = cls._read_text_from_file(coin_prompt_path)
        
        return cls(
                coin_prompt = coin_prompt,
                schedule_prompt = schedule_prompt,
                **kwargs 
                )

    def _prompt_model(self, prompt, data = []):
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


    def _assert_has_attr(self, attr:str):
        
        assert getattr(self, attr), f"'{self.__class__.__name__}' does not have the attribute '{attr}'"
    
    def get_info(self, message):
        """
        This funtion information about the schedule of the pump by 
        looking at the message. If there is no information about a pump, the model ignores the message.

        Parameters: 
        ----------
        message: str
            The message to be checked
        
        Returns: 
        ----------
            str: A string with information about the pump if one is detected, ideally in JSON format (depending on the prompt)
        """
        self._assert_has_attr('schedule_prompt')
        return self._prompt_model(self.schedule_prompt, [message])

    def get_coin(self, messages):

        """

        This function looks at a list of messages and determines whether the name of 
        the currency being pumped is mentioned. Should only be called when information about 
        the schedule of a pump is already known.

        Parameters:
        ----------
        messages: Iterable[str]
            The list of messages to be checked

        Returns:
        ----------
        str: String with the model's response for the name of the coin, output format depends on the prompt 
        
        """
        self._assert_has_attr('coin_prompt')
        return self._prompt_model(self.coin_prompt, messages)





class GeminiDetector(PumpDetector):

    def __init__(self, api_key, schedule_prompt = None, coin_prompt = None):
        
        super().__init__(coin_prompt = coin_prompt, schedule_prompt = schedule_prompt)
        
        # Import here so it is not necessary to have this package istalled in case any other detector is used
        import google.generativeai as genai
        genai.configure(api_key = api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def _prompt_model(self, prompt, data = []):

        result = self.model.generate_content(
            [prompt, *data]
        )
        return result.text





if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')


    detector  = GeminiDetector.from_prompt_path(
            api_key = config['gemini-flash']['API_KEY'],
            schedule_prompt_path = 'prompts/prompt-test.txt',
            coin_prompt_path = 'prompts/coin-prompt.txt'
        )
    print(detector.get_info(GeminiDetector._read_text_from_file('test-messages/schedule.txt')))
    
    # Do this for the coin detection model
    # prompt = prompt.replace('||EXCHANGE||', exchange)






