import { Box, Flex, Card, HStack, Text } from "@chakra-ui/react";

export default function RecentPosts() {
  return (
    <div>
      <Box bg="#EDF7FA" height="400px">
        <Text fontWeight="400" fontSize="22px" color="#21243D" ml="148px">
          Recent Posts
        </Text>
        <Flex gap="8" direction="row" justify="center">
          <Card.Root width="420px" bg="white" color="#21243D" mt="64px">
            <Card.Header />
            <Card.Body>
              <Card.Title fontWeight="700" fontSize="26px">
                Making a design system from scratch
              </Card.Title>
              <Flex
                gap="8"
                align="center"
                direction="row"
                justify="center"
                mt="10px"
              >
                <Text fontWeight="400" fontSize="18px">
                  12 Feb 2020
                </Text>
                <Text fontWeight="400" fontSize="18px">
                  |
                </Text>
                <Text fontWeight="400" fontSize="18px">
                  Design, Pattern
                </Text>
              </Flex>

              <Card.Description mt="16px">
                Amet minim mollit non deserunt ullamco est sit aliqua dolor do
                amet sint. Velit officia consequat duis enim velit mollit.
                Exercitation veniam consequat sunt nostrud amet.
              </Card.Description>
            </Card.Body>

            <Card.Footer />
          </Card.Root>
          <Card.Root width="420px" bg="white" color="#21243D" mt="64px">
            <Card.Header />
            <Card.Body>
              <Card.Title fontWeight="700" fontSize="26px">
                Creating pixel perfect icons in Figma
              </Card.Title>
              <Flex
                gap="8"
                align="center"
                direction="row"
                justify="center"
                mt="10px"
              >
                <Text fontWeight="400" fontSize="18px">
                  12 Feb 2020
                </Text>
                <Text fontWeight="400" fontSize="18px">
                  |
                </Text>
                <Text fontWeight="400" fontSize="18px">
                  Figma, Icon Design
                </Text>
              </Flex>
              <Card.Description mt="16px">
                Amet minim mollit non deserunt ullamco est sit aliqua dolor do
                amet sint. Velit officia consequat duis enim velit mollit.
                Exercitation veniam consequat sunt nostrud amet.
              </Card.Description>
            </Card.Body>
            <Card.Footer />
          </Card.Root>
        </Flex>
      </Box>
    </div>
  );
}
