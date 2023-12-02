import { Button, HStack, Textarea, VStack } from "@chakra-ui/react";
import { useState } from "react";

const InputWindow = ({ handleCorrect }: any) => {
  const [text, setText] = useState("");

  const MAX_TEXT_LENGTH = 500;

  const handleClear = () => {
    setText("");
  };

  const changeText = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (e.target.value.length > MAX_TEXT_LENGTH) {
      e.target.value = e.target.value.slice(0, MAX_TEXT_LENGTH);
    }
    setText(e.target.value);
  };

  return (
    <VStack alignItems="flex-end">
      <Textarea
        placeholder="Wpisz tekst do poprawy..."
        resize="none"
        width={{ base: "15em", md: "20em", lg: "30em" }}
        fontSize="2xl"
        cursor="auto"
        _focus={{
          boxShadow: "0 0 0 1px #667EEA",
        }}
        height="8em"
        value={text}
        onChange={changeText}
      ></Textarea>
      <HStack>
        <Button onClick={handleClear}>Wyczyść</Button>

        <Button
          isDisabled
          cursor="default"
          _active={{}}
          _disabled={{}}
          _hover={{}}
          w="5em"
        >
          {text.length}/{MAX_TEXT_LENGTH}
        </Button>
        <Button onClick={() => handleCorrect(text)}>Korekta</Button>
      </HStack>
    </VStack>
  );
};

export default InputWindow;
