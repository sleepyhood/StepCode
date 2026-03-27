using System;
using System.Threading.Tasks;
using Windows.Storage;
using Windows.Storage.Streams;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using System.Runtime.InteropServices.WindowsRuntime;
public static class WinOcrHelper {
  public static string ReadText(string path) {
    return ReadTextAsync(path).GetAwaiter().GetResult();
  }
  public static async Task<string> ReadTextAsync(string path) {
    var file = await StorageFile.GetFileFromPathAsync(path);
    using (IRandomAccessStream stream = await file.OpenAsync(FileAccessMode.Read)) {
      var decoder = await BitmapDecoder.CreateAsync(stream);
      var bitmap = await decoder.GetSoftwareBitmapAsync();
      var engine = OcrEngine.TryCreateFromUserProfileLanguages();
      var result = await engine.RecognizeAsync(bitmap);
      return result.Text;
    }
  }
}
