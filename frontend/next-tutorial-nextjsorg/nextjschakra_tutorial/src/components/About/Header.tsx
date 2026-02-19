import { Box, Heading, Text, Button, HStack, Image } from "@chakra-ui/react";
import { Avatar } from "@/components/ui/avatar";
export default function Header() {
  return (
    <div>
      <Box
        bg="white"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <HStack>
          <Box bg="white">
            <Heading
              as="h1"
              mt="228px"
              ml="148px"
              color="#21243D"
              fontWeight="700"
              fontSize="44px"
            >
              Hi, I am Ajit,
            </Heading>
            <Heading
              as="h1"
              mt="25px"
              ml="148px"
              color="#21243D"
              fontWeight="700"
              fontSize="44px"
            >
              Full Stack Developer
            </Heading>
            <Text
              fontWeight="400"
              fontSize="16px"
              textWrap="balance"
              color="#21243D"
              mt="20px"
              ml="148px"
              width="500px"
              lineClamp="3"
            >
              Amet minim mollit non deserunt ullamco est sit aliqua dolor do
              amet sint. Velit officia consequat duis enim velit mollit.
              Exercitation veniam consequat sunt nostrud amet.
            </Text>
            <Button size="lg" colorPalette="red" mt="25px" ml="148px" mb="50px">
              Download Resume
            </Button>
          </Box>
          <Box bg="white">
            {/* <Avatar
              size="2xl"
              name="Ajit"
              src="https://gravatar.com/avatar/cc8fb0ede6e0050148c5078f4fac4573?s=400&d=robohash&r=x"
            /> */}
            <Image
              src="https://gravatar.com/avatar/f4836eeece2012510172a22f3885a5bd?s=800&d=robohash&r=x"
              boxSize="300px"
              borderRadius="full"
              fit="cover"
              alt="Kumar Ajit"
            />
          </Box>
        </HStack>
      </Box>
    </div>
  );
}
