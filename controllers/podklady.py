# coding: utf8

@auth.requires_login()
def seznam():
    return dict(grid=SQLFORM.grid(db.podklad,
              deletable=False,
              editable=auth.has_membership('admin'),
              create=auth.has_membership('admin'),
              csv=auth.has_membership('admin'),
              paginate=100,
              ))
