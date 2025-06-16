import NavbarMenuItem from './NavbarMenuItem.jsx'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'
import { useAppData } from './AppDataContext.jsx'
import Loading from './Loading.jsx'

function Navbar() {
    const { data, projects, models, runs, selectedProject, selectedModel, selectedRun } = useAppData();
    if (!projects) {
        return Loading;
    }

    return (
        <nav className="w-full h-14 bg-light-foreground rounded-xl m-6 drop-shadow-lg/90 flex items-center p-2 z-40">
            <div>
                <img
                    src="/logo.png"
                    alt="Profile"
                    className="w-14 h-14 p-2 rounded-full object-cover"
                />
            </div>
            <div className="flex w-full h-3/4 ml-4 mr-2 justify-between">
                <NavbarMenuItem name="Projects" items={projects} selected={selectedProject}/>
                <NavbarMenuItem name="Models" items={models} selected={selectedModel}/>
                <NavbarMenuItem name="Runs" items={runs} selected={selectedRun}/>
            </div>
        </nav>
    )
}
export default Navbar;
