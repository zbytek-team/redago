import { Flex } from "@chakra-ui/react";
import Header from "./components/Header";
import InputWindow from "./components/InputWindow";
import OutputWindow from "./components/OutputWindow";
import { useState } from "react";

import Correct from "./services/correct";

type ResponseWord = {
  text: string;
  corrected: string;
  reason: string[];
};

const App = () => {
  const [responseText, setResponseText] = useState([] as ResponseWord[]);

  const handleCorrect = (text: string) => {
    Correct(text)
      .then((response) => {
        if (response.status === 201) {
          setResponseText(response.data.tokenized_text);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <Flex flexDirection="column" alignItems="center">
      <Flex
        bgGradient="linear(to-r, #764BA2, #667EEA)"
        w="100%"
        color="white"
        boxShadow="lg"
      >
        <Header />
      </Flex>
      <Flex
        marginTop="100px"
        flexDirection={{ base: "column", "2xl": "row" }}
        gap="20px"
      >
        <InputWindow handleCorrect={handleCorrect} />
        <OutputWindow responseText={responseText} />
      </Flex>
    </Flex>
  );
};

export default App;
