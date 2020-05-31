# The PCB-Tester-Framework Application Interface

The `applications` are thus [conda]() packages that expose funcionality to the `PCB-Tester-Framework`.

The 'exposing' is done base on [pluggy](https://github.com/pytest-dev/pluggy).

<ins>Let it be clear</ins>, the `application` does **not** handle **any** user interaction itself! That is handled by the `PCB-Tester-Framework` on behalf of the `application`. This way, the [user interface](https://github.com/ate-org/PCB-Tester/blob/master/software/UserInterface.md) can change **without** the need to 'touch up' all previous implemented `applications`.
