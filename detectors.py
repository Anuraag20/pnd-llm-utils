
import configparser

import google.generativeai as genai

class PumpDetectorInterface:
    
    
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
        
        assert hasattr(self, attr) and getattr(self, attr), f"'{self.__class__.__name__}' does not have the attribute '{attr}'"
    
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





class GeminiDetector(PumpDetectorInterface):

    def __init__(self, api_key, schedule_prompt = None, coin_prompt = None):

        genai.configure(api_key = api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.schedule_prompt = schedule_prompt
        self.coin_prompt = coin_prompt

    def _prompt_model(self, prompt, data = []):

        result = self.model.generate_content(
            [prompt, *data]
        )
        return result.text



def read_text_from_file(path):

    with open(path, 'r') as f:
        text = ''.join(f.readlines())
    return text


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    schedule_prompt = read_text_from_file('prompts/prompt-test.txt')
    coin_prompt = read_text_from_file('prompts/coin-prompt.txt')
    schedule_message = read_text_from_file('test-messages/schedule.txt')

    detector  = GeminiDetector(
            api_key = config['gemini-flash']['API_KEY'],
            schedule_prompt = schedule_prompt,
            coin_prompt = coin_prompt
        )
    print(detector.get_info(schedule_message))

    # Do this for the coin detection model
    # prompt = prompt.replace('||EXCHANGE||', exchange)






