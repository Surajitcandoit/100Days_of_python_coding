#!/usr/bin/env python3
import os
import json
import shlex
import csv
import time

# ======================
# UI / Colors
# ======================
rest = "\033[0m"
clrs = [
    "\033[91m",  # 0 Red
    "\033[92m",  # 1 Green
    "\033[93m",  # 2 Yellow
    "\033[94m",  # 3 Blue
    "\033[95m",  # 4 Magenta
    "\033[96m"   # 5 Cyan
]


def color(text, code_idx=2, end=rest):
    print(f"{clrs[code_idx]}{text}{end}")


# ======================
# Data model
# ======================
class Contact:
    def __init__(self, name, number, group=None, email=None):
        self.name = name
        self.number = number
        self.group = group
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "number": self.number,
            "group": self.group,
            "email": self.email
        }

    @staticmethod
    def from_dict(d):
        return Contact(d["name"], d["number"], d.get("group"), d.get("email"))


# ======================
# Storage & Operations
# ======================
class ContactList:
    """
    Stores data in a single JSON file with structure:
    {
      "contacts": { "Alice": {...}, ... },
      "groups": { "friends": ["Alice", "Bob"], ... }
    }
    """
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.data = {"contacts": {}, "groups": {}}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.data = json.load(f)
            except Exception:
                color("Failed to load contacts file — starting fresh.", 0)
                self.data = {"contacts": {}, "groups": {}}
        else:
            self.data = {"contacts": {}, "groups": {}}

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=2)

    # ---- contact operations ----
    def add(self, name, number, group=None, email=None, overwrite=False):
        key = name
        if key in self.data["contacts"] and not overwrite:
            color(f"Contact '{name}' already exists. Use overwrite=True to replace.", 0)
            return False
        c = Contact(name, number, group, email)
        self.data["contacts"][key] = c.to_dict()

        # auto-add to group if provided
        if group:
            self.data["groups"].setdefault(group, [])
            if key not in self.data["groups"][group]:
                self.data["groups"][group].append(key)

        self.save()
        color(f"Contact '{name}' saved.", 1)
        return True

    def delete(self, name):
        if name not in self.data["contacts"]:
            color(f"Contact '{name}' not found.", 0)
            return False
        # remove from groups
        for g, members in self.data["groups"].items():
            if name in members:
                members.remove(name)
        del self.data["contacts"][name]
        self.save()
        color(f"Contact '{name}' deleted.", 1)
        return True

    def rename(self, old_name, new_name):
        if old_name not in self.data["contacts"]:
            color(f"Contact '{old_name}' not found.", 0)
            return False
        if new_name in self.data["contacts"]:
            color(f"Contact '{new_name}' already exists.", 0)
            return False
        self.data["contacts"][new_name] = self.data["contacts"].pop(old_name)
        self.data["contacts"][new_name]["name"] = new_name
        # update groups
        for g, members in self.data["groups"].items():
            for i, m in enumerate(members):
                if m == old_name:
                    members[i] = new_name
        self.save()
        color(f"Renamed '{old_name}' -> '{new_name}'.", 1)
        return True

    def edit(self, name):
        if name not in self.data["contacts"]:
            color(f"Contact '{name}' not found.", 0)
            return False
        c = Contact.from_dict(self.data["contacts"][name])
        color("Leave field blank to keep current value.", 3)
        new_name = input(f"New name [{c.name}]: ").strip() or c.name
        new_number = input(f"New number [{c.number}]: ").strip() or c.number
        new_group = input(f"New group [{c.group}]: ").strip() or c.group
        new_email = input(f"New email [{c.email}]: ").strip() or c.email

        # if renaming, ensure no collision and update groups
        if new_name != name:
            if new_name in self.data["contacts"]:
                color(f"Cannot rename: '{new_name}' exists.", 0)
                return False
            self.rename(name, new_name)
            name = new_name

        # update fields
        self.data["contacts"][name].update({
            "number": new_number,
            "group": new_group,
            "email": new_email
        })

        # manage group membership: ensure contact in its named group (if set)
        # remove from other groups (we'll keep membership simple: the contact's group field indicates a primary group,
        # but we also keep explicit group membership lists; keep them consistent)
        # First remove from all groups then add to new_group if set
        for g in list(self.data["groups"].keys()):
            if name in self.data["groups"][g]:
                self.data["groups"][g].remove(name)
        if new_group:
            self.data["groups"].setdefault(new_group, [])
            if name not in self.data["groups"][new_group]:
                self.data["groups"][new_group].append(name)

        self.save()
        color(f"Contact '{name}' updated.", 1)
        return True

    def search(self, keyword):
        k = keyword.lower()
        results = []
        for name, d in self.data["contacts"].items():
            if k in name.lower() or k in d.get("number", "").lower() or (d.get("email") and k in d.get("email").lower()):
                results.append(d)
        if not results:
            color(f"No matches for '{keyword}'.", 0)
        else:
            color(f"Found {len(results)} result(s):", 3)
            for c in results:
                print_contact_summary(c)

    def show(self, sortby="name"):
        contacts = list(self.data["contacts"].values())
        if not contacts:
            color("No contacts saved.", 0)
            return
        if sortby == "name":
            contacts.sort(key=lambda x: x["name"].lower())
        elif sortby == "number":
            contacts.sort(key=lambda x: x.get("number", ""))
        color(f"Contacts ({len(contacts)}):", 4)
        for c in contacts:
            print_contact_summary(c)

    def display_contact_details(self, name):
        if name not in self.data["contacts"]:
            color(f"Contact '{name}' not found.", 0)
            return
        c = self.data["contacts"][name]
        color(f"Name   : {c.get('name')}", 5)
        color(f"Number : {c.get('number')}", 5)
        color(f"Group  : {c.get('group')}", 5)
        color(f"Email  : {c.get('email')}", 5)
        # list explicit groups that include this contact
        in_groups = [g for g, members in self.data["groups"].items() if name in members]
        color(f"Member of groups: {', '.join(in_groups) if in_groups else '—'}", 3)

    # ---- group operations ----
    def create_group(self, group_name):
        if group_name in self.data["groups"]:
            color(f"Group '{group_name}' already exists.", 0)
            return False
        self.data["groups"][group_name] = []
        self.save()
        color(f"Group '{group_name}' created.", 1)
        return True

    def delete_group(self, group_name):
        if group_name not in self.data["groups"]:
            color(f"Group '{group_name}' not found.", 0)
            return False
        del self.data["groups"][group_name]
        self.save()
        color(f"Group '{group_name}' deleted.", 1)
        return True

    def rename_group(self, old, new):
        if old not in self.data["groups"]:
            color(f"Group '{old}' not found.", 0)
            return False
        if new in self.data["groups"]:
            color(f"Group '{new}' already exists.", 0)
            return False
        self.data["groups"][new] = self.data["groups"].pop(old)
        # also change group's name field for contacts whose 'group' field equals old
        for name, d in self.data["contacts"].items():
            if d.get("group") == old:
                d["group"] = new
        self.save()
        color(f"Group '{old}' renamed to '{new}'.", 1)
        return True

    def add_contact_to_group(self, group, contact_name):
        if contact_name not in self.data["contacts"]:
            color(f"Contact '{contact_name}' not found.", 0)
            return False
        self.data["groups"].setdefault(group, [])
        if contact_name in self.data["groups"][group]:
            color(f"'{contact_name}' already in group '{group}'.", 0)
            return False
        self.data["groups"][group].append(contact_name)
        self.save()
        color(f"Added '{contact_name}' to '{group}'.", 1)
        return True

    def remove_contact_from_group(self, group, contact_name):
        if group not in self.data["groups"] or contact_name not in self.data["groups"][group]:
            color(f"'{contact_name}' not present in group '{group}'.", 0)
            return False
        self.data["groups"][group].remove(contact_name)
        self.save()
        color(f"Removed '{contact_name}' from '{group}'.", 1)
        return True

    def show_group(self, group_name=None):
        if group_name is None:
            # list groups
            if not self.data["groups"]:
                color("No groups created.", 0)
                return
            color(f"Groups ({len(self.data['groups'])}):", 4)
            for g, members in self.data["groups"].items():
                print(f"  - {g} ({len(members)} member(s))")
            return
        if group_name not in self.data["groups"]:
            color(f"Group '{group_name}' not found.", 0)
            return
        members = self.data["groups"][group_name]
        color(f"Members of '{group_name}' ({len(members)}):", 3)
        if not members:
            color("  (no members)", 0)
        for m in members:
            self.display_contact_details(m)

    # ---- import / export ----
    def export_csv(self, filename="contacts_export.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "number", "group", "email"])
            for c in self.data["contacts"].values():
                writer.writerow([c.get("name", ""), c.get("number", ""), c.get("group", ""), c.get("email", "")])
        color(f"Exported contacts to {filename}", 1)

    def import_csv(self, filename="contacts_import.csv", skip_existing=True):
        if not os.path.exists(filename):
            color(f"File '{filename}' not found.", 0)
            return
        imported = 0
        with open(filename, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name") or row.get("Name")
                number = row.get("number") or row.get("Number")
                group = row.get("group") or row.get("Group")
                email = row.get("email") or row.get("Email")
                if not name or not number:
                    continue
                if name in self.data["contacts"] and skip_existing:
                    continue
                self.add(name, number, group, email, overwrite=not skip_existing)
                imported += 1
        color(f"Imported {imported} contact(s) from {filename}", 1)


# ======================
# Helpers & CLI UI
# ======================
def print_contact_summary(c):
    nm = c.get("name", "")
    num = c.get("number", "")
    grp = c.get("group") or "-"
    email = c.get("email") or "-"
    print(f"{clrs[2]}Name:{nm:25}\n{clrs[5]}Number:{num:15}\n{clrs[3]}group:{grp:12}\nemail:{email}{rest}")


MAIN_HELP = """
Main commands (at prompt `contact>>`):
  show [name|--sort name|--sort number]      Show all contacts or contact by exact name
  add <name> <number> [group] [email]       Add a contact
  del <name>                                 Delete a contact
  rename <old_name> <new_name>               Rename a contact
  edit <name>                                Interactive edit for a contact
  search <keyword>                           Search contacts by name/number/email (partial, case-insensitive)
  group                                      Enter group mode (prompt becomes contact/group>>)
  show groups                                List all groups
  export [filename]                          Export contacts to CSV (default contacts_export.csv)
  import <filename>                          Import contacts from CSV (name,number,group,email)
  count                                      Show number of contacts and groups
  help                                       Show this help
  exit                                       Quit program

Notes:
- You can type an exact contact name at the prompt to see details.
- Many commands accept simple optional args; use 'help' for quick reminders.
"""

GROUP_HELP = """
Group commands (at prompt `contact/group>>`):
  show                  Show groups summary
  show <group_name>     Show members of a group (with details)
  add <group_name>      Create a new group
  del <group_name>      Delete a group
  rename <old> <new>    Rename a group (keeps members)
  <group> add <name>    Add existing contact <name> to <group>
  <group> del <name>    Remove <name> from <group>
  back                  Return to main prompt
  help                  Show this help
  exit                  Quit program
"""


def main_loop():
    cl = ContactList()
    color("Welcome to Contacts Manager — type 'help' for commands.", 5)

    while True:
        try:
            raw = input("contact>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not raw:
            continue
        parts = shlex.split(raw)
        cmd = parts[0].lower()

        # immediate-exit
        if cmd == "exit" or cmd =="q":
            break

        # help
        if cmd == "help":
            color(MAIN_HELP, 2)
            continue

        # show
        if cmd == "show":
            # show groups?
            if len(parts) >= 2 and parts[1] in ("groups", "group", "--groups"):
                cl.show_group()
                continue
            # sort option
            if len(parts) >= 3 and parts[1] == "--sort":
                cl.show(sortby=parts[2])
                continue
            # show a specific contact by exact name
            if len(parts) == 2:
                name = parts[1]
                if name in cl.data["contacts"]:
                    cl.display_contact_details(name)
                else:
                    color(f"No contact named '{name}'.", 0)
                continue
            cl.show()  # default
            continue

        # add
        if cmd == "add":
            if len(parts) < 3:
                color("Usage: add <name> <number> [group] [email]", 0)
                continue
            name = parts[1]
            number = parts[2]
            group = parts[3] if len(parts) >= 4 else None
            email = parts[4] if len(parts) >= 5 else None
            cl.add(name, number, group, email)
            continue

        # delete
        if cmd in ("del", "delete"):
            if len(parts) != 2:
                color("Usage: del <name>", 0)
                continue
            name = parts[1]
            confirm = input(f"Confirm delete '{name}'? (y/N): ").strip().lower()
            if confirm == "y":
                cl.delete(name)
            else:
                color("Delete cancelled.", 2)
            continue

        # rename contact
        if cmd == "rename":
            if len(parts) != 3:
                color("Usage: rename <old_name> <new_name>", 0)
                continue
            cl.rename(parts[1], parts[2])
            continue

        # edit
        if cmd == "edit":
            if len(parts) != 2:
                color("Usage: edit <name>", 0)
                continue
            cl.edit(parts[1])
            continue

        # search
        if cmd == "search":
            if len(parts) != 2:
                color("Usage: search <keyword>", 0)
                continue
            cl.search(parts[1])
            continue

        # group -> enter sub-loop
        if cmd == "group":
            group_loop(cl)
            continue

        # export / import
        if cmd == "export":
            filename = parts[1] if len(parts) >= 2 else "contacts_export.csv"
            cl.export_csv(filename)
            continue

        if cmd == "import":
            if len(parts) != 2:
                color("Usage: import <filename>", 0)
                continue
            cl.import_csv(parts[1])
            continue

        # count
        if cmd == "count":
            ccount = len(cl.data["contacts"])
            gcount = len(cl.data["groups"])
            color(f"{ccount} contact(s), {gcount} group(s).", 3)
            continue

        # if user typed exact contact name, show details
        if raw in cl.data["contacts"]:
            cl.display_contact_details(raw)
            continue

        color("Unknown command. Type 'help' for commands.", 0)


def group_loop(contact_list: ContactList):
    color("Entering group mode. Type 'help' for group commands, 'back' to return.", 5)
    while True:
        try:
            raw = input("contact/group>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not raw:
            continue
        parts = shlex.split(raw)
        cmd = parts[0].lower()

        if cmd == "exit" or cmd == "q":
            # Quit entire program
            raise SystemExit

        if cmd == "back":
            return

        if cmd == "help":
            color(GROUP_HELP, 3)
            continue

        if cmd == "show":
            if len(parts) == 1:
                contact_list.show_group()
                continue
            # show specific group
            contact_list.show_group(parts[1])
            continue

        if cmd == "add":
            if len(parts) != 2:
                color("Usage: add <group_name>", 0)
                continue
            contact_list.create_group(parts[1])
            continue

        if cmd in ("del", "delete"):
            if len(parts) != 2:
                color("Usage: del <group_name>", 0)
                continue
            contact_list.delete_group(parts[1])
            continue

        if cmd == "rename":
            if len(parts) != 3:
                color("Usage: rename <old> <new>", 0)
                continue
            contact_list.rename_group(parts[1], parts[2])
            continue

        # pattern: <group> add <name>  or <group> del <name>
        if len(parts) == 3 and parts[1] in ("add", "del"):
            groupname = parts[0]
            op = parts[1]
            cname = parts[2]
            if op == "add":
                contact_list.add_contact_to_group(groupname, cname)
            else:
                contact_list.remove_contact_from_group(groupname, cname)
            continue

        # pattern: <group> add <name> (alternative)
        if len(parts) == 4 and parts[1] in ("add", "del") and parts[0] in contact_list.data["groups"]:
            # e.g. groupname add name
            groupname = parts[0]
            op = parts[1]
            cname = parts[2]
            if op == "add":
                contact_list.add_contact_to_group(groupname, cname)
            else:
                contact_list.remove_contact_from_group(groupname, cname)
            continue

        # direct group op: groupname add name
        # fallback parse: <group> add/del <name>
        if len(parts) >= 3 and parts[1] in ("add", "del"):
            groupname = parts[0]
            op = parts[1]
            cname = parts[2]
            if op == "add":
                contact_list.add_contact_to_group(groupname, cname)
            else:
                contact_list.remove_contact_from_group(groupname, cname)
            continue

        color("Unknown group command. Type 'help'.", 0)


if __name__ == "__main__":
    try:
        main_loop()
    except SystemExit:
        color("Goodbye!", 5)
    except KeyboardInterrupt:
        print()
        color("Goodbye!", 5)
