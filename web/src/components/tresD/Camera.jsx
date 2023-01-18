import * as THREE from "three";
import { useState, useEffect } from "react";
import { useThree } from "@react-three/fiber";
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";

export default function Camera(props) {
  const [room, setRoom] = useState(props.room);
  const [apartment, setApartment] = useState(props.apartment);

  const set = useThree((state) => state.set);
  const { size } = useThree();

  useEffect(() => {
    setRoom(props.room);
    setApartment(props.apartment);
    set({
      camera: new THREE.PerspectiveCamera(50, size.width / size.height, 0.1, 200),
    });
  }, [props.room, props.apartment]);

  const { camera } = useThree();

  if (room) {
    camera.position.x = -5;
    camera.position.y = 4;
    camera.position.z = 7;
  } else if (apartment) {
    camera.position.x = -9;
    camera.position.y = 13;
    camera.position.z = 13;
  }

  return (
    <>
      <PerspectiveCamera makeDefault />
      <OrbitControls enableDamping={true} />
    </>
  );
}
