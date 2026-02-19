import { Button } from "@/components/ui/button";
import { HStack, Stack } from "@chakra-ui/react";
import { Slider } from "@/components/ui/slider";
export default function Home() {
  return (
    <HStack>
      <Button>Click me</Button>
      <Button>Click me</Button>
      <Stack width="200px" gap="4">
        <Slider defaultValue={[40]} size="sm" label="slider - sm" />
        <Slider defaultValue={[40]} size="md" label="slider - md" />
        <Slider defaultValue={[40]} size="lg" label="slider - lg" />
      </Stack>
      <Stack gap="4" align="flex-start">
        <Slider width="200px" colorPalette="gray" defaultValue={[40]} />
        <Slider width="200px" colorPalette="blue" defaultValue={[40]} />
        <Slider width="200px" colorPalette="red" defaultValue={[40]} />
        <Slider width="200px" colorPalette="green" defaultValue={[40]} />
        <Slider width="200px" colorPalette="pink" defaultValue={[40]} />
        <Slider width="200px" colorPalette="teal" defaultValue={[40]} />
        <Slider width="200px" colorPalette="purple" defaultValue={[40]} />
        <Slider width="200px" colorPalette="cyan" defaultValue={[40]} />
      </Stack>
    </HStack>
  );
}
