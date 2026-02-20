import React from "react";
import { useForm, useFieldArray, FormProvider } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, Button, Accordion, AccordionItem } from "@heroui/react";
import { Icon } from "@iconify/react";
import { jobExperienceSchema, type JobExperienceFormData } from "../types/job-experience";
import { JobEntryForm } from "./JobEntryForm";

export function JobExperienceForm() {
  const methods = useForm<JobExperienceFormData>({
    resolver: zodResolver(jobExperienceSchema),
    defaultValues: {
      experiences: [],
    },
  });

  const { handleSubmit } = methods;
  const { fields, append, remove } = useFieldArray({
    control: methods.control,
    name: "experiences",
  });

  const onSubmit = (data: JobExperienceFormData) => {
    console.log(data);
  };

  const addNewExperience = () => {
    append({
      id: crypto.randomUUID(),
      companyName: "",
      jobTitle: "",
      location: "",
      startDate: "",
      currentlyWorking: false,
      description: "",
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
            Job Experience
          </h1>
          <Button
            color="primary"
            startContent={<Icon icon="lucide:plus" />}
            onPress={addNewExperience}
          >
            Add Job Experience
          </Button>
        </div>

        {fields.length > 0 ? (
          <Accordion>
            {fields.map((field, index) => (
              <AccordionItem
                key={field.id}
                aria-label={`Job Experience ${index + 1}`}
                title={`Job Experience ${index + 1}`}
                subtitle={field.jobTitle || "New Entry"}
              >
                <JobEntryForm
                  index={index}
                  onRemove={() => remove(index)}
                />
              </AccordionItem>
            ))}
          </Accordion>
        ) : (
          <div className="text-center py-8 text-default-400">
            No job experiences yet. Click the button above to add one.
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
            Save Experiences
          </Button>
        </div>
      </Form>
    </FormProvider>
  );
}