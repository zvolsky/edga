# coding: utf8

@auth.requires_login()
def seznam():
    return dict(grid=SQLFORM.grid(db.lista,
              deletable=False,
              editable=auth.has_membership('admin'),
              create=auth.has_membership('admin'),
              csv=auth.has_membership('admin'),
              paginate=100,
              ))
              #fields=(db.auth_user.vs, db.auth_user.ss,
              #    db.auth_user.organizator,
              #    db.auth_user.nick, db.auth_user.zaloha,
              #    db.auth_user.first_name, db.auth_user.last_name,
              #    db.auth_user.email, db.auth_user.email_ver,
              #    db.auth_user.telefon, db.auth_user.tel_ver,
              #    db.auth_user.prihlasen,
              #    db.auth_user.neposilat, db.auth_user.ne_ostatnim,
              #    db.auth_user.id
              #    ),
              #orderby=db.auth_user.nick.lower(),
              #maxtextlengths={'auth_user.email' : 30}
