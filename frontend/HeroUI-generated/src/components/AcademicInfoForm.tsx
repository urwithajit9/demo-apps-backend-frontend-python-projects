import React from "react";
import { useForm, useFieldArray, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, Button, Accordion, AccordionItem } from "@heroui/react";
import { Icon } from "@iconify/react";
import { academicInfoSchema, type AcademicInfoFormData } from "../types/academic-info";
import { AcademicEntryForm } from "./AcademicEntryForm";

export function AcademicInfoForm() {
  const methods = useForm<AcademicInfoFormData>({
    resolver: zodResolver(academicInfoSchema),
    defaultValues: {
      academics: [],
    },
  });

  const { handleSubmit } = methods;
  const { fields, append, remove } = useFieldArray({
    control: methods.control,
    name: "academics",
  });

  const onSubmit = (data: AcademicInfoFormData) => {
    console.log(data);
  };

  const addNewAcademic = () => {
    append({
      id: crypto.randomUUID(),
      degree: "",
      fieldOfStudy: "",
      institution: "",
      startDate: "",
      currentlyStudying: false,
      publications: [],
    });
  };

  return (
    <FormProvider {...methods}>
      <Form 
        className="space-y-6 bg-content1 p-8 rounded-lg shadow-lg"
        onSubmit={handleSubmit(onSubmit)}
      >
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold text-foreground">
            Academic Information
          </h1>
          <Button
            color="primary"
            startContent={<Icon icon="lucide:plus" />}
            onPress={addNewAcademic}
          >
            Add Academic Entry
          </Button>
        </div>

        {fields.length > 0 ? (
          <Accordion>
            {fields.map((field, index) => (
              <AccordionItem
                key={field.id}
                aria-label={`Academic Entry ${index + 1}`}
                title={`Academic Entry ${index + 1}`}
                subtitle={field.degree || "New Entry"}
              >
                <AcademicEntryForm
                  index={index}
                  onRemove={() => remove(index)}
                />
              </AccordionItem>
            ))}
          </Accordion>
        ) : (
          <div className="text-center py-8 text-default-400">
            No academic entries yet. Click the button above to add one.
          </div>
        )}

        <div className="flex justify-end gap-4">
          <Button
            type="button"
            variant="flat"
            color="default"
            startContent={<Icon icon="lucide:x" />}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            color="primary"
            startContent={<Icon icon="lucide:save" />}
            isDisabled={fields.length === 0}
          >
            Save Academic Info
          </Button>
        </div>
      </Form>
    </FormProvider>
  );
}