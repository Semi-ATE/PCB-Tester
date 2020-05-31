# The PCB-Tester-Framework Application Interface

The `applications` are thus [conda]() packages that expose funcionality to the `PCB-Tester-Framework`.

The 'exposing' is done base on [pluggy](https://github.com/pytest-dev/pluggy)
Let it be clear, the `application` does **not** handle **any** user interaction! That is handled by the `PCB-Tester-Framework`. This way, the [user interface](https://github.com/ate-org/PCB-Tester/blob/master/software/UserInterface.md) can change **without** the need to 'touch up' all previous implemented `applications`.
