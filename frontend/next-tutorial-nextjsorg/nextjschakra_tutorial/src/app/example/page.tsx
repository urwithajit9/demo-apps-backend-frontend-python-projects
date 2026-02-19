import { Box } from "@chakra-ui/react";

export default function Example() {
  return (
    <div>
      <Box
        width="15em"
        border="1px solid #333"
        boxShadow="8px 8px 5px #444"
        padding="8px 12px"
        backgroundImage="linear-gradient(180deg, #fff, #ddd 40%, #ccc)"
      >
        Heres a very interesting note displayed in a lovely shadowed box.
      </Box>
    </div>
  );
}
