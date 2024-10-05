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
        raise NotImplementedError("The function '_prompt_model' needs to be implemented by ", self.__class__)

    def _assert_has_attr(self, attr:str):

        assert hasattr(self, attr), f"'{self.__class__.__name__}' does not have the attribute '{attr}'"
    
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
        return self._prompt_model(self.coin_prompt, [message])

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



