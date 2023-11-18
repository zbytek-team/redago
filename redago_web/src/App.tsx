import {
  Box,
  Button,
  Center,
  HStack,
  Heading,
  Textarea,
  VStack,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";

function App() {
  const [sentences, setSentences] = useState<string>("");
  const [corrected_sentences, setCorrectedSentences] = useState<string>("");
  const [lettersAmount, setLettersAmount] = useState<number>(0);

  const handleCorrect = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    fetch("http://localhost:8000/corrector", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: sentences }),
    })
      .then((response) => response.json())
      .then((data) => setCorrectedSentences(data.corrected_sentences));
  };

  const handleCopy = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    navigator.clipboard.writeText(corrected_sentences);
  };

  const handleClearSentences = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setSentences("");
    setLettersAmount(0);
  };

  const handleClearCorrected = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setCorrectedSentences("");
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    e.preventDefault();

    let text = e.target.value;

    // trim text to 500 letters
    if (text.length > 500) {
      text = text.slice(0, 500);
    }
    setSentences(text);
  };

  useEffect(() => {
    setLettersAmount(sentences.length);
  }, [sentences]);

  return (
    <>
      <Box padding="1em" boxShadow="md">
        <Heading size="2xl" color="blue.500">
          Korekcjoner
        </Heading>
      </Box>
      <Center height="60vh" minHeight="35em" justifyContent="center">
        <VStack flexDirection={{ base: "column", "2xl": "row" }} gap="1em">
          <VStack alignItems="flex-end">
            <Textarea
              placeholder="Wstaw tekst do korekty"
              value={sentences}
              onChange={handleInputChange}
              width={{ base: "15em", md: "20em", lg: "30em" }}
              resize="none"
              colorScheme="facebook"
              fontSize="2xl"
              cursor="auto"
              height="8em"
            ></Textarea>
            <HStack>
              <Button onClick={handleClearSentences}>Wyczyść</Button>

              <Button
                isDisabled
                cursor="default"
                _active={{}}
                _disabled={{}}
                _hover={{}}
                w="5em"
              >
                {lettersAmount}/500
              </Button>
              <Button onClick={handleCorrect} colorScheme="blue">
                Korekta
              </Button>
            </HStack>
          </VStack>

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
              <Button onClick={handleClearCorrected}>Wyczyść</Button>
              <Button onClick={handleCopy}>Kopiuj</Button>
            </HStack>
          </VStack>
        </VStack>
      </Center>
    </>
  );
}

export default App;
