import {
  ProSidebar,
  Menu,
  MenuItem,
  SidebarHeader,
  SidebarFooter,
  SidebarContent,
} from "react-pro-sidebar";
import { useContext } from "react";
import RouterLink from "next/link";
import { Flex, Image, IconButton } from "@chakra-ui/react";
import UIContext from "../core/providers/UIProvider/context";
import React from "react";
import { HamburgerIcon, ArrowLeftIcon, ArrowRightIcon } from "@chakra-ui/icons";
import { MdTimeline, MdSettings } from "react-icons/md";
import { ImStatsBars } from "react-icons/im";

const Sidebar = () => {
  const ui = useContext(UIContext);
  return (
    <ProSidebar
      width="240px"
      breakPoint="lg"
      toggled={ui.sidebarToggled}
      onToggle={ui.setSidebarToggled}
      collapsed={ui.sidebarCollapsed}
      hidden={!ui.sidebarVisible}
    >
      <SidebarHeader>
        <Flex>
          <IconButton
            ml={4}
            justifySelf="flex-start"
            colorScheme="primary"
            aria-label="App navigation"
            icon={
              ui.isMobileView ? (
                <HamburgerIcon />
              ) : ui.sidebarCollapsed ? (
                <ArrowRightIcon />
              ) : (
                <ArrowLeftIcon />
              )
            }
            onClick={() => {
              ui.isMobileView
                ? ui.setSidebarToggled(!ui.sidebarToggled)
                : ui.setSidebarCollapsed(!ui.sidebarCollapsed);
            }}
          />
          <Image
            // as={Link}
            // to="/"
            w="150px"
            py="0.75rem"
            pl={5}
            src="/icons/bugout-dev-white.svg"
            alt="bugout.dev"
          />
        </Flex>
      </SidebarHeader>
      <SidebarContent>
        <Menu iconShape="square">
          <MenuItem icon={<MdTimeline />}>
            {" "}
            <RouterLink href="/stream">Stream</RouterLink>
          </MenuItem>
        </Menu>
        <Menu iconShape="square">
          <MenuItem icon={<ImStatsBars />}>
            {" "}
            <RouterLink href="/analytics">Analytics </RouterLink>
          </MenuItem>
        </Menu>
        <Menu iconShape="square">
          <MenuItem icon={<MdSettings />}>
            {" "}
            <RouterLink href="/subscriptions">Subscriptions </RouterLink>
          </MenuItem>
        </Menu>
      </SidebarContent>
      <SidebarFooter>
        {/**
         *  You can add a footer for the sidebar ex: copyright
         */}
      </SidebarFooter>
    </ProSidebar>
  );
};

export default Sidebar;
