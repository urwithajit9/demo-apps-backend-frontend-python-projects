import React from "react";
import { Tabs, Tab } from "@heroui/react";
import { JobExperienceForm } from "./components/JobExperienceForm";
import { PersonalInfoForm } from "./components/PersonalInfoForm";
import { AcademicInfoForm } from "./components/AcademicInfoForm";

export default function App() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <Tabs aria-label="User Information Forms" color="primary">
          <Tab key="personal" title="Personal Information">
            <PersonalInfoForm />
          </Tab>
          <Tab key="academic" title="Academic Information">
            <AcademicInfoForm />
          </Tab>
          <Tab key="experience" title="Job Experience">
            <JobExperienceForm />
          </Tab>
        </Tabs>
      </div>
    </div>
  );
}