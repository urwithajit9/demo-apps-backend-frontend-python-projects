"use client";
import React, { useState } from "react";
import {
  Box,
  Button,
  Input,
  Text,
  VStack,
  HStack,
  Heading,
} from "@chakra-ui/react";

function Addition() {
  const [num1, setNum1] = useState("");
  const [num2, setNum2] = useState("");
  const [result, setResult] = useState(null);

  const handleAdd = () => {
    const sum = parseFloat(num1) + parseFloat(num2);
    setResult(sum);
  };

  return (
    <Box
      bg="gray.50"
      minH="100vh"
      display="flex"
      justifyContent="center"
      alignItems="center"
      padding="4"
    >
      <Box
        bg="white"
        p="6"
        rounded="lg"
        shadow="lg"
        borderWidth="1px"
        borderColor="gray.200"
        maxWidth="sm"
        width="100%"
      >
        <Heading as="h1" size="lg" textAlign="center" mb="4">
          Add Two Numbers
        </Heading>
        <VStack spacing="4">
          <Input
            placeholder="Enter first number"
            value={num1}
            onChange={(e) => setNum1(e.target.value)}
            type="number"
          />
          <Input
            placeholder="Enter second number"
            value={num2}
            onChange={(e) => setNum2(e.target.value)}
            type="number"
          />
          <Button colorScheme="teal" onClick={handleAdd} width="100%">
            Add Numbers
          </Button>
        </VStack>
        {result !== null && (
          <Text fontSize="lg" textAlign="center" mt="4" color="teal.600">
            Result: {result}
          </Text>
        )}
      </Box>
    </Box>
  );
}

export default Addition;
