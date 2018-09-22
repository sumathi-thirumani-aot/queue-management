'''Copyright 2018 Province of British Columbia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.'''


from app.models import CSR
from flask import flash, redirect, request
from flask_admin.contrib.sqla import ModelView
from flask_admin.babel import gettext
from flask_admin.base import expose
from flask_admin.form import FormOpts
from flask_admin.helpers import get_redirect_target
from flask_admin.model.helpers import get_mdict_item_or_list
from flask_login import current_user
from qsystem import db


class CSRConfig(ModelView):
    roles_allowed = ['GA', 'HELPDESK', 'SUPPORT']

    def is_accessible(self):
        print (current_user.role.role_code)
        return current_user.is_authenticated and current_user.role.role_code in self.roles_allowed

    create_modal = False
    edit_modal = False

    @property
    def can_create(self):
        return current_user.role.role_code != 'GA'

    can_delete = False

    column_list = ['username', 'office.office_name', 'role.role_desc', 'deleted']
    column_labels = {
        'username': 'Username',
        'office.office_name': 'Office',
        'role.role_desc': 'Role',
        'deleted': 'Deleted'
    }
    column_sortable_list = ('username', 'office.office_name', 'role.role_desc', 'deleted')
    column_default_sort = 'username'
    form_args = {
        'qt_xn_csr_ind': {'default': '0'},
        'receptionist_ind': {'default': '0'},
        'csr_state': {'default': 'Logout'}
    }
    form_excluded_columns = ('periods',)
    form_create_rules = ('username', 'qt_xn_csr_ind', 'receptionist_ind', 'csr_state', 'role', 'office','deleted',)
    form_edit_rules = ('username', 'qt_xn_csr_ind', 'receptionist_ind', 'csr_state', 'role', 'office', 'deleted',)

    @expose('/edit/', methods=('GET', 'POST'))
    def edit_view(self):
        """
            Edit model view
        """
        return_url = get_redirect_target() or self.get_url('.index_view')

        if not self.can_edit:
            return redirect(return_url)

        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)

        model = self.get_one(id)

        if model is None:
            flash(gettext('Record does not exist.'), 'error')
            return redirect(return_url)

        form = self.edit_form(obj=model)
        if not hasattr(form, '_validated_ruleset') or not form._validated_ruleset:
            self._validate_form_instance(ruleset=self._form_edit_rules, form=form)

        if self.validate_form(form):
            if self.update_model(form, model):
                flash(gettext('''Record was successfully saved. 
                Note: it may take up to 5 minutes for these changes to be effective'''), 'success')
                if '_add_another' in request.form:
                    return redirect(self.get_url('.create_view', url=return_url))
                elif '_continue_editing' in request.form:
                    return redirect(request.url)
                else:
                    # save button
                    return redirect(self.get_save_return_url(model, is_created=False))

        if request.method == 'GET' or form.errors:
            self.on_form_prefill(form, id)

        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        if self.edit_modal and request.args.get('modal'):
            template = self.edit_modal_template
        else:
            template = self.edit_template

        return self.render(template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)


CSRModelView = CSRConfig(CSR, db.session)
