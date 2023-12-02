import { Container, Flex, Center, VStack } from "@chakra-ui/react";
import Header from "./components/Header";
import InputWindow from "./components/InputWindow";
import OutputWindow from "./components/OutputWindow";

const App = () => {
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
        <InputWindow />
        <OutputWindow />
      </Flex>
    </Flex>
  );
};

export default App;
