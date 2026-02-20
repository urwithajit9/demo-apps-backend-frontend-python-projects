import React from "react";
import { useFormContext } from "react-hook-form";
import { Input, Textarea, Switch, Button } from "@heroui/react";
import { Icon } from "@iconify/react";
import type { JobExperienceFormData } from "../types/job-experience";

interface JobEntryFormProps {
  index: number;
  onRemove: () => void;
}

export function JobEntryForm({ index, onRemove }: JobEntryFormProps) {
  const {
    register,
    watch,
    formState: { errors },
  } = useFormContext<JobExperienceFormData>();

  const currentlyWorking = watch(`experiences.${index}.currentlyWorking`);
  const jobErrors = errors.experiences?.[index];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Input
          label="Company Name"
          placeholder="Enter company name"
          errorMessage={jobErrors?.companyName?.message}
          isInvalid={!!jobErrors?.companyName}
          {...register(`experiences.${index}.companyName`)}
          startContent={
            <Icon 
              icon="lucide:building" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Job Title"
          placeholder="Enter job title"
          errorMessage={jobErrors?.jobTitle?.message}
          isInvalid={!!jobErrors?.jobTitle}
          {...register(`experiences.${index}.jobTitle`)}
          startContent={
            <Icon 
              icon="lucide:briefcase" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          label="Location"
          placeholder="Enter location"
          errorMessage={jobErrors?.location?.message}
          isInvalid={!!jobErrors?.location}
          {...register(`experiences.${index}.location`)}
          startContent={
            <Icon 
              icon="lucide:map-pin" 
              className="text-default-400 pointer-events-none flex-shrink-0"
            />
          }
        />

        <Input
          type="date"
          label="Start Date"
          placeholder="Select start date"
          errorMessage={jobErrors?.startDate?.message}
          isInvalid={!!jobErrors?.startDate}
          {...register(`experiences.${index}.startDate`)}
        />

        <div className="flex items-center gap-4">
          <Switch
            {...register(`experiences.${index}.currentlyWorking`)}
          >
            I currently work here
          </Switch>
        </div>

        {!currentlyWorking && (
          <Input
            type="date"
            label="End Date"
            placeholder="Select end date"
            errorMessage={jobErrors?.endDate?.message}
            isInvalid={!!jobErrors?.endDate}
            {...register(`experiences.${index}.endDate`)}
          />
        )}
      </div>

      <Textarea
        label="Description"
        placeholder="Describe your responsibilities and achievements"
        errorMessage={jobErrors?.description?.message}
        isInvalid={!!jobErrors?.description}
        {...register(`experiences.${index}.description`)}
        minRows={4}
      />

      <Button
        type="button"
        color="danger"
        variant="flat"
        startContent={<Icon icon="lucide:trash-2" />}
        onPress={onRemove}
      >
        Remove Job Entry
      </Button>
    </div>
  );
}