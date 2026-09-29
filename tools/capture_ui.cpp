// Render the actual Qt widgets offline; this is not a robot controller.
#include <autolabor_operator_gui/main_window.h>
#include <ros/ros.h>
#include <QApplication>
#include <QDir>
#include <QFont>
#include <QLineEdit>
#include <QPixmap>
#include <QSpinBox>
#include <QTabWidget>
#include <QTimer>
#include <functional>
#include <iostream>

int main(int argc, char** argv)
{
  const QString destination = argc > 1 ? QString::fromLocal8Bit(argv[1])
                                      : QStringLiteral("docs/screenshots");
  // The preview always uses an unused loopback endpoint, independent of the
  // operator's real ROS environment. It never starts a ROS master or backend.
  qputenv("ROS_MASTER_URI", "http://127.0.0.1:1");
  qputenv("ROS_IP", "127.0.0.1");
  qunsetenv("ROS_HOSTNAME");
  QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
  QApplication::setAttribute(Qt::AA_UseHighDpiPixmaps);
  ros::init(argc, argv, "qt_ui_design_capture",
            ros::init_options::AnonymousName | ros::init_options::NoSigintHandler);
  QApplication app(argc, argv);
  QFont font = app.font();
  font.setPointSizeF(13.0);
  app.setFont(font);
  autolabor_operator_gui::MainWindow window;
  // The original sweep panel automatically queries once on startup. Point
  // that read-only query at loopback before processing any Qt timer events.
  window.findChild<QLineEdit*>("sweepAddress")->setText("127.0.0.1");
  window.findChild<QSpinBox*>("sweepPort")->setValue(1);
  QTabWidget* pages = nullptr;
  for (auto* tabs : window.findChildren<QTabWidget*>())
    if (tabs->count() == 7 && tabs->tabText(0) == QStringLiteral("综合"))
      pages = tabs;
  if (!pages || !QDir().mkpath(destination))
    return 2;
  window.resize(1680, 1000);
  window.show();
  const QStringList names = {"01_overview", "02_gps", "03_remote", "04_test",
                             "05_vision", "06_sweep", "07_logs"};
  int index = 0;
  std::function<void()> capture;
  capture = [&]() {
    pages->setCurrentIndex(index);
    QTimer::singleShot(400, &app, [&]() {
      const QString file = QDir(destination).filePath(names.at(index) + ".png");
      if (!window.grab().save(file))
      {
        app.exit(3);
        return;
      }
      std::cout << file.toStdString() << std::endl;
      if (++index == names.size())
        app.quit();
      else
        capture();
    });
  };
  QTimer::singleShot(700, &app, capture);
  const int result = app.exec();
  ros::shutdown();
  return result;
}
