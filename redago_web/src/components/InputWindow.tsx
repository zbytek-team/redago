import { Button, HStack, Textarea, VStack } from "@chakra-ui/react";

const InputWindow = () => {
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
      ></Textarea>
      <HStack>
        <Button>Wyczyść</Button>

        <Button
          isDisabled
          cursor="default"
          _active={{}}
          _disabled={{}}
          _hover={{}}
          w="5em"
        >
          0/500
        </Button>
        <Button>Korekta</Button>
      </HStack>
    </VStack>
  );
};

export default InputWindow;
