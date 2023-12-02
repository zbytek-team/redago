import { Box, Button, HStack, Tooltip, VStack } from "@chakra-ui/react";
import { useState, useEffect } from "react";

interface ResponseWord {
  text: string;
  corrected: string;
  reason: string[];
}

const tooltipDict: { [key: string]: string } = {
  case: "Zdanie powinno zaczynać się z dużej litery.",
  comma: "Wstawienie przecinka.",
  nocomma: "Usunięcie zbędnego przecinka.",
  period: "Wstawienie kropki na końcu zdania.",
  ortography: "Błąd ortograficzny albo literówka.",
};

interface OutputWindowProps {
  responseText: ResponseWord[];
}

const OutputWindow: React.FC<OutputWindowProps> = ({ responseText }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
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
        height="8em"
      >
        {responseText.map((word) => {
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
