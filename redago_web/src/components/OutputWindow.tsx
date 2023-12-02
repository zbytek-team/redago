import { Box, Button, HStack, Textarea, VStack } from "@chakra-ui/react";
import React from "react";

const OutputWindow = ({ corrected_sentences }: any) => {
  const handleCopy = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    navigator.clipboard.writeText(corrected_sentences);
  };

  return (
    <VStack alignItems="flex-end">
      <Textarea
        placeholder="Poprawiony tekst"
        isDisabled
        value={corrected_sentences}
        width={{ base: "15em", md: "20em", lg: "30em" }}
        resize="none"
        variant="filled"
        fontSize="2xl"
        color="black"
        cursor="auto"
        _disabled={{}}
        _hover={{}}
        height="8em"
      ></Textarea>
      <HStack>
        <Button onClick={handleCopy}>Kopiuj</Button>
      </HStack>
    </VStack>
  );
};

export default OutputWindow;
