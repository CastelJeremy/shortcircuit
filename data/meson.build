pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'shortcircuit')
gnome = import('gnome')

gnome.compile_resources('shortcircuit',
  'in.bharatkalluri.shortcircuit.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_file = i18n.merge_file(
  input: 'in.bharatkalluri.shortcircuit.desktop.in',
  output: 'in.bharatkalluri.shortcircuit.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'in.bharatkalluri.shortcircuit.appdata.xml.in',
  output: 'in.bharatkalluri.shortcircuit.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('in.bharatkalluri.shortcircuit.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

install_data(
    'icons/'+'in.bharatkalluri.shortcircuit'+'.svg',
    install_dir: join_paths(join_paths(get_option('datadir'), 'icons/hicolor'), 'scalable/apps')
)

