import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faCaretDown } from '@fortawesome/free-solid-svg-icons'

function NavbarMenuItem({name = "Sample", items = ["Item 1", "Item 2", "Item 3"]}) {
    return (
        <Menu as="div" className="w-80 bg-primary-translucent rounded-full p-4 flex items-center relative">
            <div className="w-full">
                <MenuButton className="flex w-full items-center justify-between">
                    <div className="text-text-color text-lg font-semibold">
                        {name}
                    </div>
                    <FontAwesomeIcon className="text-text-color" icon={faCaretDown} />
                </MenuButton>
            </div>
            <MenuItems
                transition
                className="absolute z-50 top-10 w-5/6 bg-white rounded-lg transition focus:ring-0 focus:ring-offset-0 data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in"
            >
                <div className="py-1">
                    {items.map((item, index) => (
                        <MenuItem key={index}>
                            <a
                                href="#"
                                className="block px-4 py-2 text-sm text-gray-700 data-focus:bg-primary-translucent data-focus:text-gray-900 data-focus:outline-hidden"
                            >
                                {item}
                            </a>
                        </MenuItem>
                    ))}
                </div>
            </MenuItems>
        </Menu>
    )
}
export default NavbarMenuItem;
