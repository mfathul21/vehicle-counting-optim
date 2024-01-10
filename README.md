<h1>TRAFFIC LIGHT OPTIMIZATION USING VEHICLE COUNTING & FUZZY LOGIC</h1>

<h2>Background Permasalahan</h2>
<p>
  Di Indonesia, beberapa wilayah telah berkembang menjadi daerah perkotaan dengan pertumbuhan penduduk yang pesat. Pertumbuhan ini membawa dampak pada mobilitas yang tinggi
  dan kepadatan penduduk di daerah perkotaan, meningkatkan jumlah kendaraan yang berlalu lalang setiap harinya. Situasi ini menyebabkan persimpangan jalan menjadi titik
  rawan kemacetan lalu lintas. <br>
  
  Walaupun sudah terdapat lampu lalu lintas untuk mengatur arus kendaraan, seringkali terjadi ketidakefisienan dalam pengaturan waktu lampu. Pembagian waktu lampu lalu
  lintas dilakukan secara merata tanpa mempertimbangkan jumlah kendaraan di masing-masing jalur. Sebagai hasilnya, jalur dengan sedikit kendaraan dapat mendapatkan lampu
  hijau lebih lama dari yang seharusnya, sementara lampu merah pada persimpangan lain menjadi semakin lama. Permasalahan ini disebabkan oleh ketidakdinamisan pengaturan
  waktu lampu lalu lintas yang belum memperhitungkan kepadatan kendaraan secara real-time. <br>
  
  Oleh karena itu, diperlukan pendekatan yang lebih cerdas dan adaptif untuk mengoptimalkan pengaturan lampu lalu lintas dan mengatasi kemacetan secara efektif. Pendekatan
  ini harus mampu mengadaptasi waktu lampu lalu lintas secara dinamis berdasarkan kepadatan kendaraan secara real-time. Ini dapat membantu meningkatkan alur lalu lintas,
  mengurangi kemacetan, dan menciptakan pengaturan waktu lampu lalu lintas yang lebih efisien sesuai dengan kondisi lalu lintas yang berubah-ubah.
</p>

<h2>Datasets</h2>
<p>
  Dataset yang digunakan dalam proyek ini berasal dari CCTV Jogja, yang dapat diakses secara online melalui tautan berikut: 
  <a href=https://cctv.jogjakota.go.id/home>https://cctv.jogjakota.go.id</a>. Pengumpulan dataset dilakukan dengan tangkap layar dari CCTV Jogja sehingga diperoleh 
  total 700 gambar, yang mencakup dua kelas, yaitu mobil dan motor. Untuk mempersiapkan dataset sebelum dilakukan pelatihan model, kami melakukan proses anotasi gambar
  menggunakan platform <a href=https://roboflow.com/>Roboflow</a>. Selain itu, dilakukan pula proses augmentasi dengan Roboflow untuk menambah variasi dataset. 
  Dengan demikian, dataset yang telah selesai diolah dan diannotasi siap digunakan untuk proses pelatihan.
</p>

<h2>Model Faster R-CNN</h2>
<p>
  Model Faster R-CNN Salah satu model dengan akurasi yang tinggi dan juga memiliki kemampuan untuk menedeteksi objek dari berbagai skala secara efektif sehingga cocok untuk
  task deteksi objek kendaraan memiliki performa akurasi yang tinggi dalam tugas object detection serta juga memiliki kemampuan untuk mendeteksi objek dengan berbagai skala
  secara efektif menggunakan piramida fitur yang menurut kami cukup sesuai dengan task yang ingin kami selesaikan. terlepas dari itu model Faster R-CNN juga memiliki
  kelemahan atau tantangan berupa penggunaan object detection dengan pembelajaran mendalam dua tahap dan karenanya. Ini memiliki langkah region proposal yang membuatnya
  lebih lambat dibandingkan dengan model lain bahkan dengan mAP yang sama. Oleh karena itu, disini kami menggunakan modifikasi pada backbone dengan menggunakan ResNet-18 yang
  memiliki efisiensi  komputasional yang lebih baik dibandingkan arsitektur yang lebih deep seperti ResNet-50 atau ResNet-101 yang juga biasa digunakan sebagai backbone pada
  model Faster R-CNN. <br />
  
  <figure>
      <img src="assets/arsitektur_model.jpg" alt="faster-rcnn model modified" width="500">
      <figcaption>
          Faster-RCNN Model Modified
      </figcaption>
  </figure> <br />

  Modifikasi yang telah dilakukan pada model Faster-RCNN adalah dengan menambahkan backbone dari model ResNet-18 (convolutional, batchnormal, relu, maxpool, layer1, 
  layer2, layer3, layer4) dengan modfikasi lanjutan penambahan layer extra basic blocks pada setiap layer 1, 2, 3, dan 4 pada backbone tersebut. <br />
  <ul>
  <li>Download model: <br>
    https://drive.google.com/drive/folders/1L419RCGY0zDCPojnsGmZsjhzgsRS1UyS?usp=sharing</li>
  </ul>
</p>

<h2>Fuzzy Logic</h2>
<p>
  
</p>

<h2>Deployment with Streamlit</h2>
<p>
  
</p>

<h2>Kesimpulan</h2>
<p>
  Mobilitas yang tinggi dan kepadatan penduduk di daerah perkotaan menyebabkan meningkatnya jumlah kendaraan. Dan persimpangan jalan menjadi titik rawan kemacetan lalu lintas. Maka untuk mengatasi masalah tersebut, tim kami menginisiasi proyek <strong>"TRAFFIC LIGHT OPTIMIZATION USING VEHICLE COUNTING & FUZZY LOGIC"</strong> dengan memanfaatkan teknologi AI yakni Object Detection yang dapat menghitung kendaraan di persimpangan untuk manajemen lalu lintas yang dapat mengoptimalkan perencanaan waktu siklus lampu lalu lintas pada persimpangan menggunakan fuzzy logic.
</p>
