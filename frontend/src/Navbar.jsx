import NavbarMenuItem from './NavbarMenuItem.jsx'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

function Navbar({projects=["Project 1", "Project 2", "Project 3"], models=["Model 1", "Model 2", "Model 3"], runs=["Run 1", "Run 2", "Run 3"]}) {
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
                <NavbarMenuItem name="Projects" items={projects}/>
                <NavbarMenuItem name="Models" items={models}/>
                <NavbarMenuItem name="Runs" items={runs}/>
            </div>
        </nav>
    )
}
export default Navbar;
