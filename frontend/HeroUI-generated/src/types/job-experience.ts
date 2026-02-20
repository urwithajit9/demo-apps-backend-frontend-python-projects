import { z } from "zod";

const jobEntrySchema = z.object({
  id: z.string(),
  companyName: z.string().min(2, "Company name must be at least 2 characters"),
  jobTitle: z.string().min(2, "Job title must be at least 2 characters"),
  location: z.string().min(2, "Location must be at least 2 characters"),
  startDate: z.string().min(1, "Start date is required"),
  endDate: z.string().min(1, "End date is required").optional(),
  currentlyWorking: z.boolean(),
  description: z.string().min(20, "Description must be at least 20 characters"),
});

export const jobExperienceSchema = z.object({
  experiences: z.array(jobEntrySchema),
});

export type JobEntryData = z.infer<typeof jobEntrySchema>;
export type JobExperienceFormData = z.infer<typeof jobExperienceSchema>;
