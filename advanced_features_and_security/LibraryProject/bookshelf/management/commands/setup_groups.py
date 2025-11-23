"""
Management command to create user groups and assign permissions.

This command creates three groups:
- Editors: Can create and edit books
- Viewers: Can only view books
- Admins: Can view, create, edit, and delete books
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Creates user groups (Editors, Viewers, Admins) and assigns appropriate permissions'

    def handle(self, *args, **options):
        # Get the ContentType for Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all Book permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        
        # Create a dictionary of permissions for easy lookup
        permissions_dict = {}
        for perm in book_permissions:
            permissions_dict[perm.codename] = perm
        
        # Create or get groups
        groups_config = {
            'Editors': ['can_create', 'can_edit', 'can_view'],
            'Viewers': ['can_view'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }
        
        for group_name, permission_codenames in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created group: {group_name}')
                )
            else:
                # Clear existing permissions and reassign
                group.permissions.clear()
                self.stdout.write(
                    self.style.WARNING(f'→ Updated group: {group_name} (cleared existing permissions)')
                )
            
            # Assign permissions to the group
            assigned_perms = []
            for codename in permission_codenames:
                if codename in permissions_dict:
                    group.permissions.add(permissions_dict[codename])
                    assigned_perms.append(codename)
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  ⚠ Permission "{codename}" not found for Book model'
                        )
                    )
            
            if assigned_perms:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Assigned permissions to {group_name}: {", ".join(assigned_perms)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Groups setup completed successfully!')
        )
        self.stdout.write(
            self.style.SUCCESS(
                'You can now manage these groups in Django admin at /admin/auth/group/'
            )
        )



