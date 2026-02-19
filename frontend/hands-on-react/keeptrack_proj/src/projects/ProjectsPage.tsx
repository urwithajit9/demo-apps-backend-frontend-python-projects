import { MOCK_PROJECTS } from "./MockProjects";
import ProjectList from "./ProjectList";
import Clock from "./Clock";
import DropdownMenu from "./DropDown";
import { Project } from "./Project";
import ExampleForm from "./ExampleForm";
import SigninForm from "./SigninForm";
import GuessTheNumber from "./GuessTheNumber";

export default function ProjectsPage() {
  const saveProject = (project: Project) => {
    console.log("Saving project:", project);
  };

  return (
    <div>
      <h1>Projects</h1>
      {/* <pre>{JSON.stringify(MOCK_PROJECTS, null, " ")}</pre>
      {MOCK_PROJECTS.map((project) => (
        <div key={project.name}>
          <h1>Project Name: {project.name}</h1>
          <p>About: {project.description}</p>
          <img src={project.imageUrl} />
          <h3>Budget:{project.budget}</h3>
          <button onClick={handleClick}>Edit</button>
        </div>
      ))} */}
      <ProjectList onSave={saveProject} projects={MOCK_PROJECTS} />
      <Clock />
      <DropdownMenu />
      <ExampleForm />
      <SigninForm />
      <GuessTheNumber />
    </div>
  );
}
