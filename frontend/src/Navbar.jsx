import NavbarMenuItem from './NavbarMenuItem.jsx'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

function Navbar() {
    return (
        <nav className="w-full h-14 bg-light-foreground rounded-xl m-6 drop-shadow-lg/90 flex items-center p-2">
            <div>
                <img
                    src="/logo.png"
                    alt="Profile"
                    className="w-14 h-14 p-2 rounded-full object-cover"
                />
            </div>
            <div className="flex w-full h-3/4 ml-4 mr-2 justify-between">
                <NavbarMenuItem />
                <NavbarMenuItem />
                <NavbarMenuItem />
            </div>
        </nav>
    )
}
export default Navbar;
