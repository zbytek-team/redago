import { Box, Button, Center, HStack, Spinner, Tooltip, VStack } from "@chakra-ui/react";
import { useState } from "react";

interface ResponseWord {
  text: string;
  corrected: string;
  reason: string[];
}

const tooltipDict: { [key: string]: string } = {
  case_changed: "Zdanie powinno zaczynać się z dużej litery.",
  comma_inserted: "Wstawienie przecinka.",
  comma_removed: "Usunięcie zbędnego przecinka.",
  period_inserted: "Wstawienie kropki na końcu zdania.",
  period_removed: "Usunięcie zbędnej kropki.",
  spelling_changed: "Błąd ortograficzny albo literówka.",
};

interface OutputWindowProps {
  responseText: ResponseWord[];
  isLoading: boolean
}

const OutputWindow: React.FC<OutputWindowProps> = ({ responseText, isLoading }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    const text = responseText.map((word) => word.corrected).join(" ");
    navigator.clipboard.writeText(text);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 3000);
  };

  return (
    <VStack alignItems="flex-end">
      <Box
        placeholder=""
        width={{ base: "15em", md: "20em", lg: "30em" }}
        resize="none"
        backgroundColor="gray.100"
        padding={{ base: "5px", md: "20px" }}
        fontSize="2xl"
        color="black"
        cursor="auto"
        _disabled={{}}
        _hover={{}}
        height="12em"
        overflow="auto"
      >
        {isLoading && (
          <Box
            position="relative"
            top="50%"
            left="50%"
            transform="translate(-50%, -50%)"
          >
            <Center>
              <Spinner
              thickness='4px'
              speed='0.65s'
              emptyColor='gray.200'
              color='blue.500'
              size='xl' />
            </Center>
          </Box>
        )}
        {!isLoading && responseText.map((word) => {
          return (
            <>
              {word.reason[0] !== "ok" && (
                <Tooltip
                  label={
                    <Box>
                      {word.reason.map((reason) => {
                        return (
                          <Box>
                            {tooltipDict[reason] ? (
                              <Box>{tooltipDict[reason]}</Box>
                            ) : (
                              <Box>{reason}</Box>
                            )}
                          </Box>
                        );
                      })}
                      <Box marginTop={2}>
                        Poprawiono "{word.text}" na "{word.corrected}".
                      </Box>
                    </Box>
                  }
                  placement="top"
                  hasArrow
                >
                  <span
                    style={{
                      backgroundColor: "rgba(255, 50, 150, 0.15)",
                      borderRadius: "5px",
                    }}
                  >
                    {word.corrected}
                  </span>
                </Tooltip>
              )}
              {word.reason[0] === "ok" && <>{word.corrected}</>}{" "}
            </>
          );
        })}
      </Box>
      <HStack>
        <Button onClick={handleCopy}>{copied ? "Skopiowano" : "Kopiuj"}</Button>
      </HStack>
    </VStack>
  );
};

export default OutputWindow;
