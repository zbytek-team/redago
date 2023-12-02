import { Text, Heading } from "@chakra-ui/react";

const Header = () => {
  return (
    <Text
      fontFamily="Pacifico"
      fontSize="5xl"
      bgGradient="linear(to-r, #ffffff, #eaeaea)"
      bgClip="text"
      p="20px"
    >
      Redago
    </Text>
  );
};

export default Header;
